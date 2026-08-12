"""Genera los iconos PWA (pwa-192x192.png, pwa-512x512.png) con el nuevo
badge SADER (squircle verde + hoja blanca + acento dorado), reemplazando
el icono anterior de la flor de "Sembrando Vida".
"""
from PIL import Image, ImageDraw
import math

def rounded_rect_mask(size, radius):
    mask = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=255)
    return mask

def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def make_icon(size, out_path):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    # Fondo: gradiente diagonal verde (22c55e -> 15803d -> 0f4c26)
    bg = Image.new("RGBA", (size, size), (0, 0, 0, 255))
    px = bg.load()
    c1 = (34, 197, 94)
    c2 = (21, 128, 61)
    c3 = (15, 76, 38)
    for y in range(size):
        for x in range(size):
            t = (x + y) / (2 * size)
            if t < 0.55:
                col = lerp_color(c1, c2, t / 0.55)
            else:
                col = lerp_color(c2, c3, (t - 0.55) / 0.45)
            px[x, y] = (col[0], col[1], col[2], 255)

    radius = int(size * 0.26)
    mask = rounded_rect_mask(size, radius)
    img.paste(bg, (0, 0), mask)

    draw = ImageDraw.Draw(img)

    # sutil borde interior
    draw.rounded_rectangle([1, 1, size - 2, size - 2], radius=radius,
                            outline=(255, 255, 255, 36), width=max(1, size // 200))

    # Hoja blanca estilizada: dos arcos que forman una hoja, con un tallo
    cx, cy = size * 0.5, size * 0.52
    leaf_r = size * 0.28
    leaf = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ld = ImageDraw.Draw(leaf)
    # Cuerpo de la hoja: pieslice orientado formando forma de gota/hoja
    bbox_l = [cx - leaf_r, cy - leaf_r, cx + leaf_r, cy + leaf_r]
    ld.pieslice(bbox_l, start=200, end=340, fill=(255, 255, 255, 247))
    ld.ellipse([cx - leaf_r * 0.05, cy - leaf_r * 0.95, cx + leaf_r * 1.05, cy + leaf_r * 0.35],
               fill=(255, 255, 255, 247))
    img.alpha_composite(leaf)

    # Vena central de la hoja
    stem_w = max(1, int(size * 0.012))
    draw.line([(cx, cy + leaf_r * 0.55), (cx, cy - leaf_r * 0.15)],
              fill=(15, 76, 38, 140), width=stem_w)

    # Acento dorado (punto superior derecho)
    acc_r = size * 0.075
    acc_cx, acc_cy = size * 0.735, size * 0.30
    draw.ellipse([acc_cx - acc_r, acc_cy - acc_r, acc_cx + acc_r, acc_cy + acc_r],
                 fill=(245, 196, 81, 255))

    img.save(out_path)
    print("saved", out_path)

if __name__ == "__main__":
    import sys
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    make_icon(192, f"{out_dir}/pwa-192x192.png")
    make_icon(512, f"{out_dir}/pwa-512x512.png")
