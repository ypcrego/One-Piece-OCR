#!/usr/bin/env python3
from paddleocr import PaddleOCR
import cv2, numpy as np
import os
import argparse

class Rect:
    def __init__(self, x1, y1, x2, y2, text):
        self.x1, self.y1, self.x2, self.y2, self.text = x1, y1, x2, y2, text
        self.center = (x1 + x2) / 2
    def __repr__(self): return self.text

def grouper(iterable):
    prev, group = None, []
    for item in iterable:
        if prev is None or abs(item.center - prev) <= 7:
            group.append(item)
        else:
            yield group; group = [item]
        prev = item.center
    if group: yield group

def main():
    parser = argparse.ArgumentParser(
        description='OCR com PaddleOCR e saída em subpasta da pasta-mãe'
    )
    parser.add_argument('-f','--file', required=True, help='imagem .jpg/.png')
    parser.add_argument('-o','--output', default=None,
                        help='pasta de saída (padrão: subpasta da pasta-mãe)')
    args = parser.parse_args()

    if not args.file.lower().endswith(('.jpg','.jpeg','.png')):
        raise SystemExit('Erro: extensão inválida')

    # 1) transforme em caminho absoluto para evitar dirname vazio :contentReference[oaicite:7]{index=7}
    file_path = os.path.abspath(args.file)
    img_dir   = os.path.dirname(file_path)
    # 2) ou use cwd caso ainda reste vazio:
    if not img_dir:
        img_dir = os.getcwd()                        # :contentReference[oaicite:8]{index=8}

    parent = os.path.basename(img_dir)               # nome da pasta-mãe :contentReference[oaicite:9]{index=9}
    out_dir = args.output or os.path.join(img_dir, parent)
    os.makedirs(out_dir, exist_ok=True)              # safe create 

    ocr    = PaddleOCR(use_angle_cls=True, lang='en')
    result = ocr.ocr(file_path, cls=True) or []

    rects = []
    for line in result:
        for box, (txt, _) in line:
            x1,y1 = box[0]; x2,y2 = box[2]
            rects.append(Rect(x1,y1,x2,y2,txt))

    rects.sort(key=lambda r: r.center)
    groups = dict(enumerate(grouper(rects),1))
    for grp in groups.values(): grp.sort(key=lambda r: r.y1)

    # grava sem agrupamento
    with open(os.path.join(out_dir,'without_grouping.txt'),'w',encoding='utf-8') as f:
        for r in rects: f.write(r.text+'\n')
    # grava com agrupamento
    with open(os.path.join(out_dir,'with_grouping.txt'),'w',encoding='utf-8') as f:
        for grp in groups.values():
            for r in grp: f.write(r.text+'\n')

    print(f'Textos salvos em: {out_dir}')

if __name__=='__main__':
    main()
