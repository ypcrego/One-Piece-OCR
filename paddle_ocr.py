#!/usr/bin/env python3
import os
import argparse
from paddleocr import PaddleOCR

class Rect:
    def __init__(self, x1, y1, x2, y2, text):
        self.x1, self.y1, self.x2, self.y2, self.text = x1, y1, x2, y2, text
        self.center = (x1 + x2) / 2
    def __repr__(self): return self.text

def grouper(iterable, threshold=7):
    prev, group = None, []
    for item in iterable:
        if prev is None or abs(item.center - prev) <= threshold:
            group.append(item)
        else:
            yield group
            group = [item]
        prev = item.center
    if group: yield group

def main():
    parser = argparse.ArgumentParser(
        description='Extrai texto de uma imagem e salva em .txt'
    )
    parser.add_argument('-f','--file', required=True, help='Imagem .jpg/.png')
    parser.add_argument('-o','--output', default=None,
                        help='Pasta de saída (padrão: subpasta texts da pasta-mãe)')
    args = parser.parse_args()

    if not args.file.lower().endswith(('.jpg','.jpeg','.png')):
        raise SystemExit('Erro: extensão inválida, use .jpg/.jpeg/.png')

    file_path = os.path.abspath(args.file)
    img_dir = os.path.dirname(file_path) or os.getcwd()
    parent = os.path.basename(img_dir)

    out_dir = args.output or os.path.join(img_dir, 'texts')
    os.makedirs(out_dir, exist_ok=True)

    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    result = ocr.ocr(file_path, cls=True) or []

    rects = []
    for line in result:
        for box, (txt, _) in line:
            x1, y1 = box[0]
            x2, y2 = box[2]
            rects.append(Rect(x1, y1, x2, y2, txt))

    rects.sort(key=lambda r: r.center)
    groups = list(grouper(rects))
    for grp in groups:
        grp.sort(key=lambda r: r.y1)

    name = os.path.splitext(os.path.basename(file_path))[0] + '.txt'
    out_txt = os.path.join(out_dir, name)

    with open(out_txt, 'w', encoding='utf-8') as f:
        for grp in groups:
            for r in grp:
                f.write(r.text + '\n')

#    print(f'[{name}] salvo em {out_dir}')

if __name__ == '__main__':
    main()
