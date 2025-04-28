#!/usr/bin/env bash

# Para cada pasta de capítulo em One_Piece
for dir in One_Piece/*/; do
    # cria subpasta texts dentro do capítulo
    mkdir -p "${dir}texts"  # comportamento -p :contentReference[oaicite:8]{index=8}

    # para cada .jpg nessa pasta
    for img in "${dir}"*.jpg; do
        # invoca o Python, direcionando saída para texts/
        python paddle_ocr.py --file "$img" --output "${dir}texts"
    done
done
