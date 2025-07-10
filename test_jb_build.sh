#!/bin/sh
jupyter-book build . --all --keep-going
if [ $? -eq 0 ]; then
  echo "[OK] Jupyter Book build succeeded."
else
  echo "[ERROR] Jupyter Book build failed."
  exit 1
fi
