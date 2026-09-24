#!/usr/bin/env bash
# Compile the CPEN 442 Assignment 1 LaTeX template to a1.pdf
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

TEX_FILE="a1-cpen442-26w1-student-template.tex"
OUT_NAME="a1"

usage() {
  echo "Usage: $0 [clean]"
  echo "  (no args)  compile ${TEX_FILE} -> ${OUT_NAME}.pdf"
  echo "  clean      remove LaTeX build artifacts"
}

clean() {
  rm -f \
    "${OUT_NAME}.aux" "${OUT_NAME}.log" "${OUT_NAME}.out" \
    "${OUT_NAME}.toc" "${OUT_NAME}.synctex.gz" "${OUT_NAME}.fls" \
    "${OUT_NAME}.fdb_latexmk" "${OUT_NAME}.pdf"
  echo "Cleaned build artifacts."
}

compile() {
  if ! command -v pdflatex >/dev/null 2>&1; then
    echo "error: pdflatex not found. Install TeX Live, e.g.:" >&2
    echo "  sudo apt install texlive-latex-recommended texlive-latex-extra latexmk" >&2
    exit 1
  fi

  if command -v latexmk >/dev/null 2>&1; then
    latexmk -pdf -interaction=nonstopmode -halt-on-error \
      -jobname="${OUT_NAME}" "${TEX_FILE}"
  else
    # Two passes so hyperref / labels settle.
    pdflatex -interaction=nonstopmode -halt-on-error \
      -jobname="${OUT_NAME}" "${TEX_FILE}"
    pdflatex -interaction=nonstopmode -halt-on-error \
      -jobname="${OUT_NAME}" "${TEX_FILE}"
  fi

  echo "Built ${SCRIPT_DIR}/${OUT_NAME}.pdf"
}

case "${1:-}" in
  "") compile ;;
  clean) clean ;;
  -h|--help) usage ;;
  *)
    echo "error: unknown argument: $1" >&2
    usage >&2
    exit 1
    ;;
esac
