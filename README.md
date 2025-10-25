# Resonant Substrate Hypothesis (RSH): A Universal Invariant Linking Information and Energy Dissipation
*Empirical evidence for a symmetry between informational and energetic decay in gravitational-wave data.*

**Author:** Jeffrey Gewirtz  
**ORCID:** 0009-0004-8500-0049  
**Version:** v11.2 — GitHub Working Edition  
**License:** CC BY 4.0 International

> **What is this?**  
> This repository hosts the open manuscript and LaTeX source for the **Resonant Substrate Hypothesis (RSH)**.  
> RSH proposes a measurable invariant linking the temporal decay of **mutual information** and **spectral energy** in dissipative systems:
>
> F = γ_MI / (2 γ_spec) ≈ 1
>
> Evidence comes from gravitational-wave strain data (e.g., GW150914), where the informational and energetic decay constants align within uncertainty.

---

## Abstract (short)
The Resonant Substrate Hypothesis (RSH) establishes an empirical invariant bridging information loss and energy dissipation in resonant, dissipative systems. Using gravitational-wave detector data, we estimate the mutual-information decay rate γ_MI and the spectral-energy decay rate γ_spec. Across detectors and events, the dimensionless ratio F = γ_MI / (2 γ_spec) concentrates near unity, indicating a symmetry between informational and energetic decay timescales. The framework integrates bootstrap CIs and Bayesian posteriors, adheres to open-science practices, and is designed for extension beyond gravitational-wave data.

---

## Files & Layout
paper/
  ├─ main.tex
  ├─ references.bib
  ├─ figures/
  ├─ RSH_Submission_Text.txt
  ├─ RSH_v11.2_Entropy_Final_Polish.docx
  └─ RSH_v11.2.pdf
LICENSE.txt

---

## How to cite this work

**Use the current Zenodo DOI (latest public archive):**  
**DOI:** https://doi.org/10.5281/zenodo.17422850

**APA**
Gewirtz, J. (2025). *Resonant Substrate Hypothesis (RSH) v10.1 — The Gewirtz Invariant: Empirical Validation Edition.* Zenodo. https://doi.org/10.5281/zenodo.17422850

**BibTeX**
@misc{gewirtz_rsh_v10_1_2025,
  author    = {Gewirtz, Jeffrey},
  title     = {Resonant Substrate Hypothesis (RSH) v10.1 — The Gewirtz Invariant: Empirical Validation Edition},
  year      = {2025},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.17422850},
  url       = {https://doi.org/10.5281/zenodo.17422850}
}

---

## Build (LaTeX)
latexmk -pdf -interaction=nonstopmode main.tex

---

## Licensing
- Manuscript & figures: CC BY 4.0 (see LICENSE.txt).  
- Code (if added later): recommend MIT License.

---

## DOI via Zenodo (later)
1. Make the repo Public (done).  
2. On Zenodo, enable GitHub integration and flip this repo ON.  
3. In GitHub, create a Release (e.g., v11.3).  
4. Zenodo auto-archives that release and mints a new DOI.  
5. Update the README “How to cite” section to the new DOI.
