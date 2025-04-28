#!/usr/bin/env bash
for dir in One_Piece/*/; do
    base=$(basename "$dir")
    outdir="${dir%/}/${base}"
    mkdir -p "$outdir"
    for img in "${dir}"*.jpg; do
        python paddle_ocr.py --file "$img" --output "$outdir"
    done
done