"""Execute every supplied program and record its actual output as Python comments."""

import argparse
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
OUTPUT_MARKER = "# --- Captured output ---"
WORKER = r'''
import runpy
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

program = Path(sys.argv[1])
plot_dir = Path(sys.argv[2])
stem = program.stem.replace(" ", "_")
plot_number = 0

def save_plots(*args, **kwargs):
    global plot_number
    for number in plt.get_fignums():
        plot_number += 1
        suffix = "" if plot_number == 1 else f"_{plot_number}"
        plt.figure(number).savefig(plot_dir / f"{stem}{suffix}.png", dpi=150)
    plt.close("all")

plt.show = save_plots
runpy.run_path(str(program), run_name="__main__")
save_plots()
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true",
        help="Run all programs and compare stdout against saved comments and logs.",
    )
    args = parser.parse_args()
    output_dir = ROOT / "outputs"
    plot_dir = ROOT / "plots"
    output_dir.mkdir(exist_ok=True)
    plot_dir.mkdir(exist_ok=True)
    env = os.environ.copy()
    env.update({
        "MPLBACKEND": "Agg",
        "PYTHONHASHSEED": "0",
        "OPENBLAS_NUM_THREADS": "1",
        "OMP_NUM_THREADS": "1",
        "MKL_NUM_THREADS": "1",
        "LOKY_MAX_CPU_COUNT": "2",
    })
    programs = sorted(
        ROOT.glob("program *.txt"),
        key=lambda path: int(path.stem.split()[-1]),
    )
    if not programs:
        raise SystemExit("No program files found.")

    failures = []
    for program in programs:
        result = subprocess.run(
            [sys.executable, "-c", WORKER, str(program), str(plot_dir)],
            cwd=ROOT, env=env, capture_output=True, text=True, timeout=180,
        )
        if result.returncode:
            print(f"FAIL: {program.name}", file=sys.stderr)
            print(result.stderr, file=sys.stderr)
            failures.append(program.name)
            continue
        if result.stderr:
            print(result.stderr, file=sys.stderr, end="")

        source = program.read_text(encoding="utf-8")
        code = source.split(OUTPUT_MARKER, 1)[0].rstrip()
        comments = "\n".join(
            f"# {line}" if line else "#" for line in result.stdout.splitlines()
        )
        annotated = f"{code}\n\n{OUTPUT_MARKER}\n{comments}\n"
        log_path = output_dir / f"{program.stem.replace(' ', '_')}.txt"
        if args.check:
            if (source != annotated or not log_path.exists()
                    or log_path.read_text(encoding="utf-8") != result.stdout):
                failures.append(program.name)
                print(f"FAIL: saved output differs for {program.name}")
                continue
        else:
            program.write_text(annotated, encoding="utf-8")
            log_path.write_text(result.stdout, encoding="utf-8")
        print(f"PASS: {program.name}")

    if failures:
        raise SystemExit(f"Failed programs: {', '.join(failures)}")
    print(f"All {len(programs)} programs executed successfully.")


if __name__ == "__main__":
    main()
