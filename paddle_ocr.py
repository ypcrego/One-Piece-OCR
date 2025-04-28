from paddleocr import PaddleOCR
import cv2
import numpy as np


class Rect:
    def __init__(self, x1, y1, x2, y2, text):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.center = (x1 + x2) / 2
        self.text = text

    def __str__(self):
        return f"Rect[{self.x1}, {self.y1}, {self.x2}, {self.y2}]"

    def __repr__(self):
        return f"{self.text}, "


def grouper(iterable):
    prev = None
    group = []
    for item in iterable:
        if prev is None or abs(item.center - prev) <= 7:
            group.append(item)
        else:
            yield group
            group = [item]
        prev = item.center
    if group:
        yield group


ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Certifique-se de que os modelos estão baixados
img_path = '08.jpg'
result = ocr.ocr(img_path, cls=True) or []

rectangles = []

# ATUALIZAÇÃO: Percorrendo o novo formato
for line in result:
    for box, (text, confidence) in line:
        # box é uma lista de 4 pontos (4 x [x,y])
        x1, y1 = box[0]
        x2, y2 = box[2]
        rectangles.append(Rect(x1, y1, x2, y2, text))

print(f"Total de caixas detectadas: {len(rectangles)}")

rectangles.sort(key=lambda x: x.center)
groups = dict(enumerate(grouper(rectangles), 1))

# Organizando dentro de cada grupo
for group_id in groups:
    groups[group_id].sort(key=lambda x: x.y1)

print(groups)

# Salvando sem agrupamento
with open('without_grouping.txt', 'w+', encoding='utf-8') as fil:
    for rect in rectangles:
        fil.write(f'{rect.text}\n')

# Salvando com agrupamento
with open('with_grouping.txt', 'w+', encoding='utf-8') as fil:
    for group_id in groups:
        for rect in groups[group_id]:
            fil.write(f'{rect.text}\n')

# Desenhar as caixas na imagem
img = cv2.imread('08.jpg')

for line in result:
    for box, (text, confidence) in line:
        box = list(map(lambda x: (int(x[0]), int(x[1])), box))
        cv2.polylines(img, [np.array(box)], isClosed=True, color=(0, 255, 0), thickness=2)

cv2.imshow('Detected Text', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
