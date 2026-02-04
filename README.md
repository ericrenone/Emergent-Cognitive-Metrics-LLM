# Emergent Cognitive Metrics - LLM


Fully self-contained, Python-only, visualizes emergent metrics such as **logic**, **aesthetic**, **understanding**, and **utility** from a stochastic token stream.


This simulation demonstrates that simple, stochastic cognitive dynamics can produce emergent, interpretable metrics of logic, aesthetic sensitivity, understanding, and utility, without the need for trained models.


## Features

- **Self-contained**: No external dependencies beyond Python standard library.
- **Stochastic Simulation**: Generates power-law token streams (heavy-tailed, mimicking LLM input distributions).
- **Emergent Metrics**:
  - **Logic** – fidelity-driven reasoning
  - **Aesthetic** – entropy-driven diversity
  - **Understanding** – synthesis of logic and aesthetic
  - **Utility** – performance adjusted for entropy penalties
- **Visualization Dashboard** (Tkinter):
  - Time-series plots for logic, aesthetic, understanding, utility.
  - Phase space visualization (Logic vs Aesthetic).
  - Heatmap of token probabilities.
- **Headless CLI Mode**: Optional `--cli` argument prints final metrics.

