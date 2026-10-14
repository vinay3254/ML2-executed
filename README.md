# ML2 — executed programs

Eight machine learning lab programs from [ARK13-hub/ML2](https://github.com/ARK13-hub/ML2), source commit `1a019d1`.

Each original `program N.txt` file contains Python code followed by its actual captured stdout, with every output line prefixed by `#`. The supplied algorithms and datasets are retained. Plain output logs live in `outputs/`; figures from programs 4 and 5 live in `plots/`.

## Programs

1. Find-S and candidate elimination.
2. Rule learning with FOIL information gain.
3. Bagging and AdaBoost classification on Iris.
4. K-means clustering on Iris, with cluster plot.
5. Supplied self-organizing map example, with result plot.
6. Monte Carlo integration of x² on [0, 1].
7. Conditional probability tables for a Bayesian network.
8. Conditional probability queries and most probable explanation.

## Run

Use Python 3.12.14 and the pinned packages in `requirements.txt` to reproduce the saved results.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python run_all.py
```

Alternatively, use [uv](https://docs.astral.sh/uv/):

```bash
uv venv --python 3.12.14 .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python run_all.py
```

The runner executes each program in a separate process, captures actual stdout, refreshes output comments and logs, and saves Matplotlib figures using its noninteractive Agg backend. It retains the `.txt` filenames from the source repository; they remain executable Python files.

To verify all eight programs against their recorded outputs:

```bash
.venv/bin/python run_all.py --check
```

To run one program directly:

```bash
.venv/bin/python "program 1.txt"
```

Programs 4 and 5 call `plt.show()` when run directly. Use the runner to save their plots without a display. Numeric results and formatting may differ with other dependency versions. Program 3 reports both cross-validation and held-out test scores; program 2 reports accuracy on its training examples.

All eight programs execute successfully, and a second run matches the recorded stdout. The supplied AdaBoost code emits a scikit-learn deprecation warning for its default SAMME.R algorithm; the pinned version still supports it.
