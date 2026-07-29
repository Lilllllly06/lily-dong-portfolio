#!/bin/bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-python}"

if [ -x ".venv/bin/python" ]; then
    PYTHON_BIN=".venv/bin/python"
fi

TESTING=true "$PYTHON_BIN" -m unittest discover -s tests
