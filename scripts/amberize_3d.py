#!/usr/bin/env python3
"""Paint the 3D contribution skyline amber.

The 3D action leaves the block faces without a fill (they render black), and
omits the .fill-strong rule, so on a dark panel the skyline is invisible.
Each block is a group of three <rect>s in a fixed order: top, left face,
right face. This gives each face its amber shade and defines .fill-strong.
Safe to run repeatedly: it does nothing if the file is already painted.
"""
import re
import sys

path = sys.argv[1]
svg = open(path, encoding="utf-8").read()

if "data-amber" in svg:
    print("already amberized")
    sys.exit(0)

FACES = ["#e9ac50", "#b57f2e", "#8a5f20"]  # top, left, right
RECT = re.compile(r'<rect stroke="none"')
count = len(RECT.findall(svg))
if count == 0 or count % 3 != 0:
    sys.exit(f"unexpected block layout: {count} rects, not a multiple of 3; leaving file untouched")

i = 0


def paint(_m):
    global i
    fill = FACES[i % 3]
    i += 1
    return f'<rect fill="{fill}" stroke="none"'


svg = RECT.sub(paint, svg)
# language chart: TypeScript blue -> yellow (donut slice and legend swatch)
svg = re.sub(r"#3178c6", "#f7df1e", svg, flags=re.I)
svg = svg.replace("</style>", ".fill-strong { fill: #e9ac50; }\n</style>", 1)
svg = svg.replace("<svg ", '<svg data-amber="1" ', 1)
open(path, "w", encoding="utf-8").write(svg)
print(f"amberized {count // 3} blocks")
